import express, { Application } from 'express';
import fs from 'fs';

export class App {
  private readonly expressApp: Application;
  private port: number;
  constructor(port: number) {
    this.port = port;
    this.expressApp = express();
    this.expressApp.get('/', (_, res) => {
      res.send('hello world');
    });
  }
  public start() {
    this.expressApp.listen(this.port, () =>
      console.log(`App listening on port ${this.port}!`),
    );
  }
}
