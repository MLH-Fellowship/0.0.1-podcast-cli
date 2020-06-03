
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
            if [[ $2 == '' ]] 
            then 
                echo "podcast search: please enter a search term"
                return 1
            fi

            _podcast_search $2
            ;; 
        imfeelinglucky)
            _podcast_random
            ;;
        download) 
            if [[ $2 == '' ]]
            then
                echo "podcast download: please enter the short url of a dev.to podcast"
                return 1
            fi

            if [[ $3 == '' ]]
            then 
                _podcast_download $2 $3
            else
                _podcast_download $2 './podcast'
            fi
            ;;
        info)
            if [[ $2 == '' ]] 
            then 
                echo "podcast info: please enter the short url of a dev.to podcast"
                return 1
            fi

            _podcast_info $2
            ;;
        list)
            if [[ $2 == '' ]]
            then 
                echo "podcast list: please enter the page number"
                return 1
            fi

            if [[ $3 == '' ]]
            then 
                echo "podcast list: please enter the number of search results"
                return 1
            fi

            _podcast_list $2 $3
            ;;
        ""|-h|--help)
            echo "Usage: podcast <option>"
            echo "-h, --help\n\tShow help information"
            echo "search <search_term>\n\tSearch recent podcasts for the search term"
            echo "imfeelinglucky\n\tShow a random podcast episode"
            echo "podcast download <short_url> <?download_dir>\n\tDownload a podcast"
            echo "\tIf the download directory is missing, this will download to ./podcasts"
            echo "info <short_url>\n\tDisplay the show art and any metadata"
            echo "list <pg_num> <pg_size>\n\tBrowse the list of podcasts page by page"
            ;;
        *)
            echo "Unknown option: $opt"
            return 1
            ;;
    esac
}

