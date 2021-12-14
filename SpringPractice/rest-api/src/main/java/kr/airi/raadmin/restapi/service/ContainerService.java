package kr.airi.raadmin.restapi.service;

import kr.airi.raadmin.restapi.dto.ContainerReqDto;
import kr.airi.raadmin.restapi.dto.ContainerUdtDto;
import kr.airi.raadmin.restapi.entity.Container;
import kr.airi.raadmin.restapi.repository.ContainerRepository;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.List;
import java.util.Optional;

@Transactional
@Service
public class ContainerService {
    private ContainerRepository containerRepository;

    ContainerService(ContainerRepository containerRepository) {
        this.containerRepository = containerRepository;
    }

    @Transactional
    public Container getOne(int number) {
        return containerRepository.findById(number).get();
    }

    @Transactional
    public List<Container> getAll() {
        return containerRepository.findAll();
    }

    @Transactional
    public Container createOne(ContainerReqDto req) {
        Container container = req.toEntity();
        return containerRepository.save(container);
    }

    @Transactional
    public Optional<Container> update(int number, ContainerUdtDto containerUdtDto) {

        Optional<Container> udtContainer = containerRepository.findById(number);

        udtContainer.ifPresent(getContainer ->{
            getContainer.setContainer(containerUdtDto.getContainer());
            getContainer.setContent(containerUdtDto.getContent());
            getContainer.setPortNumber(containerUdtDto.getPortNumber());
            getContainer.setServerNumber(containerUdtDto.getServerNumber());

            containerRepository.save(getContainer);
        });
        return udtContainer;
    }

    @Transactional
    public void delete(int number) {
        Optional<Container> container = containerRepository.findById(number);
        if(container.isPresent()) {
            containerRepository.delete(container.get());
        }
    }
}
