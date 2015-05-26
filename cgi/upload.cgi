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
my $query;
eval { 
    $query     = CGI->new;
    $rh_params = parse_params( $query );

};
$rh_params->{error} = $@ if $@ ; 

if( $rh_params->{filename} and
    $rh_params->{pass} and
    $rh_params->{pass} eq 'dziwko1234' ) {

      open (OUTFILE, ">", "$upload_dir/apka") 
              or die "Couldn't open for writing: $!";
      my $numbytes = 1024;
      my $buffer;
      while (my $bytesread = read($rh_params->{filename}, $buffer, $numbytes)) {
	      print OUTFILE $buffer;
     } 
     close OUTFILE;
    
}    


print header(-type => "text/html", -status => "200 OK");

debug($rh_params);


sub debug {
print Dumper $rh_params;
print Dumper $query;

print qq|
	<html>
		<body>
			<h1>Upload newest version of app</h1>
			<form method="POST" enctype="multipart/form-data">
			 <input type="file"      name="file">
			 <input type="password"  name="pass">
			 <input type="submit" value="Upload" name="submit">
			 <a href="../apka">Pobierz aplikacje!</a>
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
	
	$rh_params->{fileame}       = $query->param('file'); 
	$rh_params->{fh}            = $query->upload('file'); 
	$rh_params->{pass}          = $query->param('pass');
	return $rh_params;
}
