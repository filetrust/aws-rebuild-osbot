import sys

# setup dependencies locally

sys.path.append('./modules/GW-Bot/modules/OSBot-AWS')
sys.path.append('./modules/GW-Bot/modules/OSBot-Utils')

# setup dependencies in github Actions

sys.path.append('../OSBot-AWS')
sys.path.append('../OSBot-Utils')


