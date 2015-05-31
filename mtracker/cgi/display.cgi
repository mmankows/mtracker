#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5
use strict;
use warnings;

use lib '../lib';
use Data::Dumper;
use CGI;
use URI::Escape;
use CGI::Pretty qw/:standard/;

use DBTools;
use Common;
use User;

# initialize database connection
my $dbh = DBTools::db_connect();

my $rh_params = {};

# parse params from query
my $query = CGI->new;
$rh_params = parse_params( $query );

# save to database
my $rah_positions = Common::get_positions( %$rh_params );
$rh_params->{error} = $@ if $@ ; 


print header(-type => "text/html", -status => "200 OK");
Common::print_rah( $rah_positions, ['user_id', 'logdate', 'step_id', 'latitude', 'longitude'], { format=> $rh_params->{format} } );

#### #### #### #### #### #### #### ##### ##### ##### ########

# parse query parameters
sub parse_params {
	my ( $query ) = shift;
	my $rh_params = {};
	
	$rh_params->{uid}    = uri_unescape $query->param('uid'); 
	$rh_params->{token}  = uri_unescape $query->param('t');

	# validate token & uid pair
	my $user = User::get_user( user_id => $rh_params->{uid} );
	return {} if not $user || not $user->{token} eq $rh_params->{token}; 

	$rh_params->{cnt}    = uri_unescape $query->param('cnt');
	$rh_params->{begin}  = uri_unescape $query->param('begin');
	$rh_params->{end}    = uri_unescape $query->param('end');
	$rh_params->{format} = uri_unescape $query->param('f') || 'json';

	$rh_params->{cnt} = 200 if $rh_params->{cnt} < 0 || $rh_params->{cnt} > 200;
	
	return $rh_params;
}

