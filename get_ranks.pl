#!/usr/bin/perl

    use strict;
    use warnings;
    use File::Basename;
	
    my $dir = $ARGV[0];

    opendir(DIR, $dir) or die $!;

    mkdir($ARGV[2]) or die "No $ARGV[2] directory, $!";

    while (my $file = readdir(DIR)) {

        # Use a regular expression to ignore files beginning with a period
        next if ($file =~ /^\./) or ($file =~ /^_/);
	
	    my $input = $dir."/".$file;

	    my @file_info = split (/\./, $file);
	
	    my $output = $ARGV[2]."/".$file_info[0]."\."."txt";
	
	    # print "$input $ARGV[1] $output \n";
	
	    system("python ./get_rank.py $input $ARGV[1] $output $ARGV[3]");
    }

    closedir(DIR);
    exit 0;


