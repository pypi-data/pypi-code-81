# JS-code for spinning up a v86-VM
VIRTUAL_MACHINE = """

if(typeof(HGVMNum) == "undefined"){HGVMNum = 0;} // note that this numbering deals with copies when reviewing answers

// A BETTER SOLUTION SHOULD PROBABLY BE FOUND, AS NOW TWO VMS WILL LOAD WHEN REVIEWING ANSWERS (AND BOTH ISOS WILL BE SENT!)


function HGMakeVM(container, biosURL, vgaBiosURL, ISOURL, memory, vMemory){
/**
* Creates a VM inside the given container (replaces inner HTML).
* The bios, vga-bios and iso are all given as URLs (normally data-URLs).
* The memory and vMemory are given in bytes.
*/
  container.innerHTML = '<div id="HGVMScreenContainer' + HGVMNum + '"><div style="white-space: pre; font: 14px monospace; line-height: 14px"></div><canvas style="display: none"></canvas></div>';
  var emulator = new V86Starter({
    memory_size: memory,
    vga_memory_size: vMemory,
    screen_container: document.getElementById("HGVMScreenContainer" + HGVMNum),
      bios: {
        url: biosURL		
      },
      vga_bios: {
        url: vgaBiosURL		
      },
      cdrom: {
        url: ISOURL		
      },
      autostart: true,
    }
  );
  var outputBuffer = ""; // buffer for serial-terminal-output
  var redirection = undefined; // a redirection function, which output from the serial terminal will be sent to
  var loggedIn = false; // initially a login is required for the serial terminal, this shows whether this has happened already
  emulator.add_listener("serial0-output-char", function(char) // note the hardcoded username root, and that '/root% ' is always considered a request for input (sort of bad, but hard to do another way (wait? (how long?)))
    {
      outputBuffer += char;
      if(outputBuffer.endsWith("login:") && !loggedIn){ // automatic login
        container.HGToTerminal("root\\n");
        loggedIn = true;
      }
      else if(outputBuffer.endsWith("/root% ") && !(redirection === undefined)){
        redirection(outputBuffer.slice(0,-7)); // remove the '/root% ' and the last line break
      }
    }
  );
  container.HGFromTerminal = function(){
    return outputBuffer;
  }
  container.HGToTerminal = function(commands){
    outputBuffer = "";
    emulator.serial0_send(commands);
  }
  container.HGRedirectOutput = function (redirector){
    redirection = redirector;
  }
  container.HGGetInnerVM = function(){
    // returns the v86 emulator object
    return emulator;
  }
  return container;
}
"""
