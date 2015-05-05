#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5 
use strict;
use warnings;

use lib '/home/eaiibgrp/mmankows/mtracker/lib';
use Data::Dumper;
use CGI;
use CGI::Pretty qw/:standard/;
use DBI;
use URI::Escape;
use MIME::Base64 ();

use DBTools;
# -d_id(string)    : device id
# -cs (string md5) : control sum
# -lat (base 65 float)
# -lon (base64 float)

# initialize database connection
my $dbh = DBTools::db_connect();

my $rh_params = {};
eval {
    # parse params from query
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


#TODO wyjebac
sub debug {
my ($rh_params) = @_;
# render response
my $sent    = Dumper($rh_params);
my $tracked = Dumper($dbh->selectall_arrayref("SELECT * from tracked_routes ORDER BY step_id DESC LIMIT 10",{Slice=>{}} ));
my $users   = Dumper($dbh->selectall_arrayref("SELECT * from users", {Slice=>{}}) );

my $example_req = 'http://student.agh.edu.pl/~mmankows/cgi-bin/track.cgi?d_id=abcd-efgh-ijkl&lon=MTEuMTIzMjI%3D&lat=MTEuMTIzMjI%3D';
s:\n:<br/>:g for ($sent, $tracked, $users);
print qq|
	<html>
		<body>
			<h1>Supported parameters list:</h1>
			<ul>
				<li><b>d_id(String)</b> - Device id</li>
				<li><b>lon(base64encoded float)</b> - Longitude</li>
				<li><b>lat(base64encoded float)</b> - Latitude</li>

			</ul>
			<h4>Example request</h4>
			<a href="$example_req">$example_req</a>
			<h4>What you sent</h4>
			$sent
			<h4>10 Latest tracked positions</h4>
			$tracked
			<h4>Registered users</h4>
			$users
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
	
	$rh_params->{latitude}  = uri_unescape $query->param('lat');
	$rh_params->{latitude}  = MIME::Base64::decode( $rh_params->{latitude} );
	
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
	
	if ( grep { not $rh_params->{$_} } qw/latitude longitude user_id/ ) {
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
