package kr.airi.raadmin.restapi.service;

import kr.airi.raadmin.restapi.dto.ServerSpecReqDto;
import kr.airi.raadmin.restapi.entity.ServerSpec;
import kr.airi.raadmin.restapi.repository.ServerSpecRepository;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.List;

@Service
public class ServerSpecService {

    private ServerSpecRepository serverSpecRepository;

    ServerSpecService(ServerSpecRepository serverSpecRepository) {
        this.serverSpecRepository = serverSpecRepository;
    }

    @Transactional
    public ServerSpec getOne(int number) {
        return serverSpecRepository.findById(number).get();
    }

    @Transactional
    public List<ServerSpec> getAll() {
        return serverSpecRepository.findAll();
    }

    @Transactional
    public ServerSpec createOne(ServerSpecReqDto req) {
        ServerSpec serverSpec = req.toEntity();
        return serverSpecRepository.save(serverSpec);
    }
}
