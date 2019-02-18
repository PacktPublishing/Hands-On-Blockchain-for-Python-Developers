import vyper
import os, json

filename = 'hello.vy'
contract_name = 'Hello'
contract_json_file = open('Hello.json', 'w')

with open(filename, 'r') as f:
    content = f.read()

current_directory = 'haha' # os.curdir

smart_contract = {}
smart_contract[current_directory] = content

format = ['abi', 'bytecode']
compiled_code = vyper.compile_codes(smart_contract, format, 'dict')

smart_contract_json = {
    'contractName': contract_name,
    'abi': compiled_code[current_directory]['abi'],
    'bytecode': compiled_code[current_directory]['bytecode']
}

json.dump(smart_contract_json, contract_json_file)

contract_json_file.close()
