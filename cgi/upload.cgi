#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5 
use strict;
use warnings;

use lib '/home/eaiibgrp/mmankows/mtracker/lib';
use Data::Dumper;
use CGI;
use CGI::Pretty qw/:standard/;
use DBI;
use MIME::Base64 ();

$CGI::POST_MAX = 1024 * 5000;
my $upload_dir = "/home/eaiibgrp/mmankows/mtracker";

my $rh_params;
eval { 
    my $query     = CGI->new;
    $rh_params = parse_params( $query );

};
$rh_params->{error} = $@ if $@ ; 

print header(-type => "text/html", -status => "200 OK");

debug($rh_params);


sub debug {
print Dumper $rh_params;

print qq|
	<html>
		<body>
			<h1>Upload newest version of app</h1>
			<form method="POST" enctype="multipart/form-data">
			 <input type="file"      id="file">
			 <input type="password" id="pass">
			 <input type="submit" value="Upload" name="submit">
		</body>
	</html>
|;
}
#### #### #### #### #### #### #### ##### ##### ##### ########
#### #### #### #### #### #### #### ##### ##### ##### ########
#### #### #### #### #### #### #### ##### ##### ##### ########

# parse query parameters
sub parse_params {
	my ( $query ) = shift;
	my $rh_params = {};
	
	$rh_params->{file}       = $query->param('file'); 
	$rh_params->{lattitude}  = $query->param('pass');
	return $rh_params;
}
