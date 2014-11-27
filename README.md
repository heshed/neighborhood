neighborhood
============

indexing neighborhood data to elasticsearch and visualize

- install
    ansible-playbook -i hosts/myhosts install.yml

- start|stop|restart es
    ansible-playbook -i hosts/myhosts es.yml --tags=start
    ansible-playbook -i hosts/myhosts es.yml --tags=stop
    ansible-playbook -i hosts/myhosts es.yml --tags=restart

- indexing
    ansible-playbook -i hosts/myhosts indexing.yml
    
- start viwer
