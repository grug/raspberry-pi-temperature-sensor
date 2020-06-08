import { config } from "dotenv";
import { createConnection, format as fmt } from "mysql";
import csv from "csvtojson";
import format from "date-fns/format";
import del from "del";

async function main() {
  config();

  const fileName = `${format(new Date(), "yyyy_MM_dd")}.csv`;
  const fileContents = await csv().fromFile(`./data/${fileName}`);

  const { date, temperature } = fileContents[0];

  const query = "INSERT INTO ?? (read_time, temperature) VALUES(?, ?)";
  const inserts = ["temperature_reads", date, temperature];
  const preparedQuery = fmt(query, inserts);

  const connection = createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
  });

  connection.query(preparedQuery, async (error, results) => {
    if (error) {
      console.log(error);
    }
  });

  await del(["./data/*.*"]);

  connection.end();
}

main();
