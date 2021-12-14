import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSliderModule } from "@angular/material/slider";
import { MatTableModule } from '@angular/material/table';
import { HttpClientModule } from '@angular/common/http';
import { TradeViewComponent } from './trade-view/trade-view.component';
import { Connection, Message } from "amqp-ts";

@NgModule({
  declarations: [
    AppComponent,
    TradeViewComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSliderModule,
    MatTableModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
