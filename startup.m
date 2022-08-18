% start up
function startup()
    addpath c:/speechres/commonmcode;
    cds('audapter_matlab');
    which Audapter; % shows that Aufapter core is there or throws error
    Audapter('deviceName', 'Focusrite USB ASIO');