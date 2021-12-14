import { Component, NgModule, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Observable, throwError } from "rxjs";
import { catchError, retry } from "rxjs/operators";
import { ServerItem, ContainerItem } from "./model/models";
import { Connection, Message } from "amqp-ts";

var connection = new Connection("amqp://10.100.0.61");
var exchange = connection.declareExchange("request");
var queue = connection.declareQueue("ebst_trade_response");
queue.bind(exchange);
queue.activateConsumer((message) => {
  console.log("Message received: " + message.getContent());
});

var msg = new Message("Test 메세지");
exchange.send(msg);

connection.completeConfiguration().then(() =>
{
  var msg2 = new Message("test2 메세지");
  exchange.send(msg2);
});

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent implements OnInit{
  title = 'RA-Admin';
  serverList:ServerItem[] = [];
  containerList:ContainerItem[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void{
    this.loadServerList();
    this.loadContainerList();
  }
  
  loadServerList() {
    this.http.get<ServerItem[]>(`http://localhost:8080/api/server-spec`, {responseType: 'json'})
    .subscribe(data => {
      this.serverList= data;
    });
  }
  loadContainerList() {
    this.http.get<ContainerItem[]>(`http://localhost:8080/api/containers`, {responseType: 'json'})
    .subscribe(data => {
      this.containerList= data;
    })
  }
}
