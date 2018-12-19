# ridge-test

## Ground Station GUI

### Dependencies
* [PySerial](https://github.com/pyserial/pyserial): Required to control the Arduino amp controller  
Installed using `pip install pyserial`
* [SoapySDR](https://github.com/pothosware/SoapySDR)
* [SoapyHackRF](https://github.com/pothosware/SoapyHackRF): Required if using HackRF

### Required Edits in Python Script
* Add `import amp_controller` at begining of script in the include section
* Replace `def set_squelch_detect(self, squelch_detect):` section with  
```python
def set_squelch_detect(self, squelch_detect):
  self.squelch_detect = squelch_detect
  if squelch_detect != 0:
    time.sleep(1)           # Wait for received command to complete
    self.blocks_file_source_0.seek(long(0),int(0))  # Restart recorded command
    self.set_TxRxSwitch(1)  # Switch flowgraph to transmit
    time.sleep(4)           # Wait for recording to be transmitted
    self.set_TxRxSwitch(0)  # Switch flowgraph to receive
    time.sleep(1)           # Wait for radio to switch
 ```
 * Replace `def set_TxRxSwitch(self, TxRxSwitch):` section with  
 ```python
 def set_TxRxSwitch(self, TxRxSwitch):
   self.TxRxSwitch = TxRxSwitch
   self.blks2_selector_0.set_input_index(int(self.TxRxSwitch))
   self.blks2_selector_0.set_output_index(int(self.TxRxSwitch))
   if TxRxSwitch == 1:
     amp_controller.tx()    # Switch amplifier to transmit
   else:
     amp_controller.rx()    # Switch amplifier to receive
```
