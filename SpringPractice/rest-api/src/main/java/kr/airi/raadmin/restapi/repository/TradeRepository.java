package kr.airi.raadmin.restapi.repository;

import kr.airi.raadmin.restapi.entity.Trade;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TradeRepository extends JpaRepository<Trade, Float> {
}
