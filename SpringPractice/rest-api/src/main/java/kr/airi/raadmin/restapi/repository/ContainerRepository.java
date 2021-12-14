package kr.airi.raadmin.restapi.repository;

import kr.airi.raadmin.restapi.entity.Container;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ContainerRepository extends JpaRepository<Container, Integer> {

}
