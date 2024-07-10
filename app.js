import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import connectDatabase from './database.js';

const app = express();
dotenv.config();

connectDatabase();

app.use(cors());




app.use(express.static("public"));
app.use(express.json());




const port = process.env.PORT;


app.listen(process.env.PORT, () => {
    console.log(`port is running at ${process.env.PORT}`)
})