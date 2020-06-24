import { config } from "dotenv";
import { createConnection, format as fmt } from "mysql";
import csv from "csvtojson";
import format from "date-fns/format";
import del from "del";

type ProbeType = "water_shallow" | "air" | "water_deep";

async function processFile(probe: ProbeType) {
  const fileName = `${format(new Date(), "yyyy_MM_dd")}-${probe}.csv`;
  const fileContents = await csv().fromFile(`./data/${fileName}`);

  const { date, temperature } = fileContents[0];

  const query =
    "INSERT INTO ?? (read_time, temperature, probe) VALUES(?, ?, ?)";
  const inserts = ["temperature_reads", date, temperature, probe];
  const preparedQuery = fmt(query, inserts);

  const connection = createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
  });

  connection.query(preparedQuery, async (error, _) => {
    if (error) {
      console.log(error);
    }
  });

  connection.end();
}

async function main() {
  config();

  await processFile("water_shallow");
  await processFile("water_deep");
  await processFile("air");

  await del(["./data/*.*"]);
}

main();
