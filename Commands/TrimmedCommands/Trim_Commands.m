% Separates RawCommands.iq into individual command IQ files


command_name = 'RESET!!!';
samp_rate = 160e3;      %Recording Sample Rate
len = 3;              %Desired length of recording
start = 1.899e5;       %Index for start of command
finish = 2.556e5;      %Index for end of command

filename = strcat(command_name,'_160ksps_437505kHz_30kOffset_filtered.iq');
samps = ceil(samp_rate*len); %Number of samples in output file

%% Load Command From File
dat = read_complex_binary(filename);   %Read data from file


%% Plot Raw Command
figure(1);
plot(1:length(dat),abs(dat));   %Plot entire file


%% Trim Command
command_start = ceil(len*samp_rate*0.75);
command_finish = command_start+(finish-start);
command = zeros(1,len*samp_rate);
command(command_start:command_finish) = dat(start:finish);


%% Increase Gain
gain = 1/max(abs(command));
command = command*gain;


%% Plot Final Command
figure(2);
plot((1:length(command))/samp_rate,abs(command));   %Plot entire file

%% Save Command
name = strcat(command_name,'_160ksps_437505kHz_30kOffset_',num2str(len),'s.iq');
write_complex_binary(command,name);
figure(1)