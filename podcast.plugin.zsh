
function _podcast_temp_echo() {
    for var in "$@" 
    do
        echo "$var"
    done
}

function _podcast_search() {
    _podcast_temp_echo $0 $@
}

function _podcast_random() {
    _podcast_temp_echo $0 $@
}

function _podcast_download() {
    _podcast_temp_echo $0 $@
}

function _podcast_info() {
    _podcast_temp_echo $0 $@
}

function _podcast_list() {
    _podcast_temp_echo $0 $@
}

function _podcast_help() {
    _podcast_temp_echo $0 $@
}

function podcast() {
    local opt=$1
    case "$opt" in
        search)
            ;; 
        imfeelinglucky)
            ;;
        download) 
            ;;
        info)
            ;;
        list)
            ;;
        ""|-h|--help)
            ;;
        *)
            echo "Unknown option: $opt"
            return 1
            ;;
    esac
}

