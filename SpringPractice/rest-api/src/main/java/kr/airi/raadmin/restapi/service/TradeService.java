package kr.airi.raadmin.restapi.service;

import kr.airi.raadmin.restapi.dto.TradeReqDto;
import kr.airi.raadmin.restapi.entity.Trade;
import kr.airi.raadmin.restapi.repository.TradeRepository;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.List;

@Transactional
@Service
public class TradeService {
    private TradeRepository tradeRepository;

    TradeService(TradeRepository tradeRepository) {
        this.tradeRepository = tradeRepository;
    }

    @Transactional
    public Trade getOne(float number) {
        return tradeRepository.findById(number).get();
    }

    @Transactional
    public List<Trade> getAll() {
        return tradeRepository.findAll();
    }

    @Transactional
    public Trade createOne(TradeReqDto req) {
        Trade trade = req.toEntity();
        return tradeRepository.save(trade);
    }
}
