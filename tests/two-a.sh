flow compose build -f yaml/pyfi.yaml 
read -p "Start agents..." cont
flow task run -n emit_one -d "1" -s ext.processors.sample.emit_one
flow task run -n emit_two -d "4" -s ext.processors.sample.emit_two
