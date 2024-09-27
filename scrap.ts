/** @format */

import * as fs from "node:fs";
import * as dotenv from "dotenv";
import { Command } from "commander";
import { chromium, BrowserContext } from "playwright";

dotenv.config();

const COOKIES_FILE_PATH = "session/cookies-ts.json";

/**
 * Save all cookies to a file.
 *
 * @param context The context whose cookies should be saved.
 */
async function saveCookies(context: BrowserContext, url: string) {
  const cookies = await context.cookies();
  fs.writeFileSync(
    COOKIES_FILE_PATH,
    JSON.stringify({ cookies, url }, null, 2)
  );
}

/**
 * Load all cookies from a file.
 *
 * @param context The context whose cookies should be loaded.
 */
async function loadCookies(context: BrowserContext) {
  const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE_PATH, "utf-8"));
  await context.addCookies(cookies.cookies);
  return cookies.url;
}

const runner = async (target: string): Promise<void> => {
  console.log("[Started]");

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
  });
  const page = await context.newPage();

  try {
    // Navigate to the desired webpage
    console.log("[Visiting page.]");
    await page.goto(
      "https://usstage241.dayforcehcm.com/MyDayforce/u/X5u8jynQL0GANx00a1oH1A/Common/"
    );

    if (fs.existsSync(COOKIES_FILE_PATH)) {
      console.log("[Loading cookies]");
      const url: string = await loadCookies(context);
      await page.goto(url);
    } else {
      // Wait for the company name input and enter the value
      await page.fill("#txtCompanyName", process.env.COMPANY_NAME || "");

      // Fill in the username and password
      await page.fill("#txtUserName", process.env.EMAIL || "");
      await page.fill("#txtUserPass", process.env.PASS || "");

      // Click the login button
      await page.click("#MainContent_loginUI_cmdLogin");

      saveCookies(context, page.url());
    }

    // Wait for Role to select
    await page.click("#evrDialog-button");

    await page
      .locator(".FeatureToolbarButton.EverestHamburger.everest-menu-toggle")
      .click();

    await page.locator("//*[contains(text(),'Org Setup')]").click();

    await page.click("//*[contains(text(),'Locations')]");

    if (target === "types") {
      console.log("[Fetching Location Types]");
      // Click on "Location Types"
      await page.click("//span[contains(text(),'Location Types')]");

      // Wait for the table rows to be visible
      const tableRows = await page.waitForSelector(
        ".dgrid-row.ui-state-default.dgrid-row-odd",
        { state: "visible" }
      );

      // Get all the rows
      const rows = await tableRows.$$eval("tr", (rows) =>
        rows.map((row) => {
          const cells = Array.from(row.querySelectorAll("td"));
          return cells.map((cell) => cell.textContent?.trim() || "");
        })
      );

      // Print cell data
      rows.forEach((cells) => {
        cells.forEach((cell) => {
          console.log(`[✅ Data]: ${cell}`);
        });
      });
    } else {
      // Click on "Location Properties"
      await page.click("//span[contains(text(),'Location Properties')]");

      await page.waitForSelector(".dgrid-row.ui-state-default", {
        state: "attached",
      });

      const allTables = await page.$$(".dgrid-row.ui-state-default");

      // Loop through each table
      for (const table of allTables) {
        // Get all the rows from the current table
        // $$: to get all matching rows
        const rows = await table.$$("tr");

        for (const row of rows) {
          const cells = await row.$$("td");

          for (const cell of cells) {
            const cellText = await cell.textContent();
            console.log(`[✅ Data]: ${cellText?.trim()}`);
          }
        }
      }
    }

    await page.waitForTimeout(1000);
  } catch (error) {
    console.error("Error:", error);
  } finally {
    await browser.close();
    console.log("[Exited]");
  }
};

// Set up the commander program
const program = new Command();

program
  .command("run")
  .requiredOption(
    "--target <target>",
    "Specify the target: types or properties"
  )
  .description("Run the script with the types or properties target")
  .action((target) => {
    runner(target?.target).catch((err) => console.error(err));
  });

// Parse the command line arguments
program.parse(process.argv);
