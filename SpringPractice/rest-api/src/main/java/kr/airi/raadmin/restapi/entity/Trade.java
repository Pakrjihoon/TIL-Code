package kr.airi.raadmin.restapi.entity;

import lombok.*;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Builder
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "trade_request")
public class Trade {

    @Id
    private float id;

    @Column(name = "order_number")
    private int orderNumber;

    @Column(name = "ticker_symbol")
    private String tickerSymbol;

    private float amount;
    private float price;
}
