package kr.airi.raadmin.restapi.controller;

import kr.airi.raadmin.restapi.dto.TradeReqDto;
import kr.airi.raadmin.restapi.entity.Trade;
import kr.airi.raadmin.restapi.service.TradeService;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class TradeController {

    private static final String EXCHANGE_NAME = "amq.fanout";
    @Autowired
    RabbitTemplate rabbitTemplate;
    private TradeService tradeService;

    @Autowired
    TradeController(TradeService tradeService) {
        this.tradeService = tradeService;
    }

    @GetMapping(value = "/trades")
    @ResponseBody
    public List<Trade> getAllTrade() {
        return tradeService.getAll();
    }

    @PostMapping(value = "/trade")
    @ResponseBody
    public Trade saveTrade(@RequestBody TradeReqDto req) {

        rabbitTemplate.convertAndSend(EXCHANGE_NAME, "sample.oingdaddy.#", req.toString());
        return tradeService.createOne(req);
    }

    @GetMapping(value = "/trade/{id}")
    @ResponseBody
    public Trade getContainer(@PathVariable("id")int number){
        return tradeService.getOne(number);
    }
}
