% Separates RawCommands.iq into individual command IQ files

filename = 'RawCommands.iq';
command_index = [2.45e5 3.55e5; 8.3e5 9.5e5; 1.42e6 1.53e6; 2.00e6 2.12e6;...
    2.59e6 2.71e6; 3.18e6 3.30e6; 3.77e6 3.89e6; 4.35e6 4.47e6;...
    4.94e6 5.06e6; 5.53e6 5.65e6; 6.12e6 6.24e6; 6.71e6 6.82e6;...
    7.29e6 7.41e6; 7.88e6 8.00e6; 8.47e6 8.59e6; 9.05e6 9.17e6;...
    9.64e6 9.76e6; 1.023e7 1.035e7];

%% Split file into commands

dat = read_complex_binary(filename);   %Read data from file
command = cell(size(command_index,1));
for k = 1:size(command_index,1)
    command{k} = dat(command_index(k,1):command_index(k,2));
end

%% Plots

figure(size(command_index,1)+1);
plot(1:length(dat),abs(dat));   %Plot entire file

%Plot each command
for k = 1:size(command_index,1)
    figure(k);
    plot(1:(command_index(k,2)-command_index(k,1)+1),abs(command{k}));
end

%% Write Commands to File
% filenames = cell(size(command_index,1));
% filenames = {command1

for k = 1:size(command_index,1)
    name = strcat('command',int2str(k),'.iq');
    write_complex_binary(command{k},name);
end