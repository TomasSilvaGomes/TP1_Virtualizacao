# KVM vs VirtualBox: Análise da Virtualização

**1.º Projeto Laboratorial de Virtualização e Centros de Dados · Universidade da Beira Interior**  
**Autores:** Tomás Gomes (M16516) e Bernardo Henriques (M16703)

Comparação experimental, num único computador (*single node*), entre **KVM (Tipo 1)** e **Oracle VirtualBox (Tipo 2)**, usando o sistema hospedeiro como referência. Foram avaliados CPU, memória, rede e armazenamento com **SysBench, iPerf3 e IOzone**.

## Arquitetura e ambiente

```text
Host — Ubuntu 24.04.5 LTS | Intel Core i5-12450H | 15 GiB RAM
Servidor iPerf3: 192.168.1.97
     ├── QEMU 8.2.2 / KVM (libvirt 10.0.0)
     │    Ubuntu Server 24.04 | 2 vCPU | 4 GiB RAM | disco 25 GiB
     │    VirtIO · rede libvirt default (normalmente NAT)
     │    VM 192.168.122.254  →  gateway 192.168.122.1
     └── VirtualBox 7.1.18
          Ubuntu Server 24.04 | 2 vCPU | 4 GiB RAM | disco 25 GiB
          NAT · VM 10.0.2.15  →  gateway 10.0.2.2
```

Os testes decorreram sequencialmente, com **uma VM ativa de cada vez**.

## Ficheiros

| Caminho | Conteúdo |
|---|---|
| [`Relatorio/`](Relatorio/) | Relatório final em PDF (formato IEEE) |
| [`resultados/execucoes/`](resultados/execucoes/) | **21 logs:** 12 de rede e 9 de IOzone |
| [`resultados/csvs/`](resultados/csvs/) | Três observações por cenário, médias e desvios-padrão|
| [`scripts/`](scripts/) | Validação dos valores e criação dos gráficos |


## Comandos dos ensaios

CPU e RAM (**SysBench**; repetidos 3 vezes por ambiente):

```bash
sysbench cpu --cpu-max-prime=20000 --threads=2 --time=30 run
sysbench memory --memory-block-size=1M --memory-total-size=10G --threads=2 run
```

Rede (**iPerf3**; servidor no host, 30 s por execução nas VMs):

```bash
iperf3 -s                                    # host
iperf3 -c 192.168.1.97 -t 30                # TCP: VM → host
iperf3 -c 192.168.122.1 -u -b 100M -R -t 30 # UDP KVM: host → VM
iperf3 -c 192.168.1.97 -u -b 100M -t 30     # UDP VirtualBox: VM → host
```

Armazenamento (**IOzone**; três execuções em cada ambiente):

```bash
iozone -I -t 2 -s 512m -r 4k -i 0 -i 1 -i 2
```
