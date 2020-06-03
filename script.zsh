
# Open a file in the VOX media player
function _vox_open_file() {
    # Retrieve the full path with a z shell expansion
    # https://linux.die.net/man/1/zshexpn
    local fullpath=$1:A

    # AppleScript separates directories with : instead of /.
    # The line "set a to POSIX file p" converts from /-separated
    # paths to :-separated paths. 
    #
    # http://www.satimage.fr/software/en/smile/external_codes/file_paths.html

    osascript << EOS
        set p to "$fullpath"
        set a to POSIX file p

        tell application "VOX"
            open a
        end tell
    
        return
EOS
}

