function [] = main( inputfile, outputfile )
%MAIN2 Summary of this function goes here
%   Detailed explanation goes here
    inputfile;
    r = rand(3,3);
    save(outputfile, 'r')
end
