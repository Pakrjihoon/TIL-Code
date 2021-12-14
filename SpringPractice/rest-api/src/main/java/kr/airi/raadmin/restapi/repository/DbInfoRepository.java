package kr.airi.raadmin.restapi.repository;

import kr.airi.raadmin.restapi.entity.DbInfo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DbInfoRepository extends JpaRepository<DbInfo, Integer> {

}
