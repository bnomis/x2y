if ( ${?_X2Y_ACTIVATED} ) then
    
    if ( ${?_PATH_BEFORE_X2Y_ACTIVATE} ) then
        setenv PATH $_PATH_BEFORE_X2Y_ACTIVATE
    endif

    if ( ${?_PYTHONPATH_BEFORE_X2Y_ACTIVATE} ) then
        if ( { eval 'test ! -z $_PYTHONPATH_BEFORE_X2Y_ACTIVATE' } ) then
            setenv PYTHONPATH $_PYTHONPATH_BEFORE_X2Y_ACTIVATE
        else
            unsetenv PYTHONPATH
        endif
    endif

    unsetenv _PATH_BEFORE_X2Y_ACTIVATE
    unsetenv _PYTHONPATH_BEFORE_X2Y_ACTIVATE
    unsetenv _X2Y_ACTIVATED
else
    echo 'Not active'
endif
    