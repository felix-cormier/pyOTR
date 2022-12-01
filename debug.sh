myfunction() {
    #do things with parameters like $1 such as
    python3 -m debugpy --listen nc20433:1081 --wait-for-client $@
}


myfunction $@ #calls `myfunction`
