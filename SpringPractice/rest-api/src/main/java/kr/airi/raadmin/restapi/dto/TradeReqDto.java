package kr.airi.raadmin.restapi.dto;

import kr.airi.raadmin.restapi.entity.Trade;
import lombok.*;

@ToString
@Builder
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class TradeReqDto {

    private float id;
    private int orderNumber;
    private String tickerSymbol;
    private float amount;
    private float price;
    private TradeReqDto tradeReqDto;

    public Trade toEntity() {
        return Trade.builder()
                .id(this.id)
                .orderNumber(this.orderNumber)
                .tickerSymbol(this.tickerSymbol)
                .amount(this.amount)
                .price(this.price)
                .build();
    }


}
