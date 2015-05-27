#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5
use strict;
use warnings;

use lib '/home/eaiibgrp/mmankows/mtracker/lib';
use Data::Dumper;
use CGI;
use URI::Escape;
use CGI::Pretty qw/:standard/;

use DBTools;
use Common;

# initialize database connection
my $dbh = DBTools::db_connect();

my $rh_params = {};

# parse params from query
my $query = CGI->new;
$rh_params = parse_params( $query );

# save to database
my $rah_positions = Common::get_positions( $rh_params->{uid}, $rh_params->{cnt} );
$rh_params->{error} = $@ if $@ ; 


print header(-type => "text/html", -status => "200 OK");
Common::print_rah( $rah_positions, ['user_id', 'logdate', 'step_id', 'latitude', 'longitude'], { format=> $rh_params->{format} } );

#### #### #### #### #### #### #### ##### ##### ##### ########

# parse query parameters
sub parse_params {
	my ( $query ) = shift;
	my $rh_params = {};
	
	$rh_params->{uid}    = uri_unescape $query->param('uid'); 
	$rh_params->{cnt}    = uri_unescape $query->param('cnt');
	$rh_params->{format} = uri_unescape $query->param('f') || 'json';

	$rh_params->{cnt} = 200 if $rh_params->{cnt} < 0 || $rh_params->{cnt} > 200;
	
	return $rh_params;
}

