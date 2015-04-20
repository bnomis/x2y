if [ $_X2Y_ACTIVATED ]; then
    
    if [ $_PATH_BEFORE_X2Y_ACTIVATE ]; then
        export PATH=$_PATH_BEFORE_X2Y_ACTIVATE
    fi

    if [ $_PYTHONPATH_BEFORE_X2Y_ACTIVATE ]; then
        if [  $_PYTHONPATH_BEFORE_X2Y_ACTIVATE != 0 ]; then
            export PYTHONPATH=$_PYTHONPATH_BEFORE_X2Y_ACTIVATE
        else
            unset PYTHONPATH
        fi
    fi

    unset _PATH_BEFORE_X2Y_ACTIVATE
    unset _PYTHONPATH_BEFORE_X2Y_ACTIVATE
    unset _X2Y_ACTIVATED
else
    echo 'Not active'
fi
    