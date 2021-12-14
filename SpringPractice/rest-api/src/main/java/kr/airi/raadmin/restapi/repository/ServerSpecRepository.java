package kr.airi.raadmin.restapi.repository;

import kr.airi.raadmin.restapi.entity.ServerSpec;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ServerSpecRepository extends JpaRepository<ServerSpec, Integer> {
}
