#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5 
use strict;
use warnings;

use lib '/home/eaiibgrp/mmankows/mtracker/lib';
use Data::Dumper;
use CGI;
use CGI::Pretty qw/:standard/;
use DBI;
use MIME::Base64 ();

use DBTools;
    my $query     = CGI->new;
    $rh_params = parse_params( $query );

    # validate parameters
    my $valid = validate_params( $rh_params );

    # save to database
    save_params($rh_params, 'tracked_routes') if $valid;
};
$rh_params->{error} = $@ if $@ ; 

print header(-type => "text/html", -status => "200 OK");

debug($rh_params);


sub debug {

print qq|
	<html>
		<body>
			<h1>Upload newest version of app</h1>
			<form method="POST">
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
	
	$rh_params->{device_id}  = uri_unescape $query->param('d_id'); 
	$rh_params->{user_id}    = did2uid( delete $rh_params->{device_id} );
	
	$rh_params->{lattitude}  = uri_unescape $query->param('lat');
	$rh_params->{lattitude}  = MIME::Base64::decode( $rh_params->{lattitude} );
	
	$rh_params->{longitude}  = uri_unescape $query->param('lon');
	$rh_params->{longitude}  = MIME::Base64::decode( $rh_params->{longitude} );
	
	return $rh_params;
}

# save haash to the table. Hash keys names must be exactly like columns' names
sub save_params {
	my ($rh_params, $table_name) = @_;
	return {} if not keys %$rh_params;
	my $query = sprintf("INSERT INTO %s (%s) VALUES (%s)",$table_name, join(',',keys %$rh_params), join(',',map { '?' } values %$rh_params));
	my $sth = $dbh->prepare($query);
	$sth->execute(values %$rh_params);
	
}

# validate parameters
sub validate_params {
	my ($rh_params) = shift;
	
	if ( grep { not $rh_params->{$_} } qw/lattitude longitude user_id/ ) {
		return undef;
	}

	return 1;
}

# get user_id based on device_id
sub did2uid {
	my( $device_id ) = shift;
	my ($user_id) = $dbh->selectrow_array("SELECT user_id FROM users WHERE device_id = '$device_id'");
	return $user_id;
}
