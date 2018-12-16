% Separates RawCommands.iq into individual command IQ files

filename = 'PingACK!_160ksps_437505kHz_30kOffset_filtered.iq';
samp_rate = 160e3;      %Recording Sample Rate
len = 0.75;              %Desired length of recording
start = 4.6e5;           %Index for start of command

samps = ceil(samp_rate*len); %Number of samples in output file

%% Load Command From File
dat = read_complex_binary(filename);   %Read data from file


%% Plot Raw Command
figure(1);
plot(1:length(dat),abs(dat));   %Plot entire file


%% Trim Command
command = dat(start:start+samps);


%% Increase Gain
gain = 1/max(abs(command))*1;
command = command*gain;


%% Plot Final Command
figure(2);
plot(1:length(command),abs(command));   %Plot entire file

%% Save Command
name = strcat('trimmed_',filename);
write_complex_binary(command,name);