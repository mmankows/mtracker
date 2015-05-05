#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5
use strict;
use warnings;

use lib '/home/eaiibgrp/mmankows/mtracker/lib';
use Data::Dumper;
use CGI;
use URI::Escape;
use CGI::Pretty qw/:standard/;
use DBI;
use JSON::XS;

use DBTools;

# initialize database connection
my $dbh = DBTools::db_connect();

my $rh_params = {};

# parse params from query
my $query     = CGI->new;
$rh_params = parse_params( $query );

# save to database
my $rah_positions = get_positions( $rh_params->{uid}, $rh_params->{cnt} );
$rh_params->{error} = $@ if $@ ; 

print header(-type => "text/html", -status => "200 OK");
print_rah( $rah_positions, ['user_id', 'logdate', 'step_id', 'lattitude', 'longitude'] );

#### #### #### #### #### #### #### ##### ##### ##### ########
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

# save haash to the table. Hash keys names must be exactly like columns' names
sub get_positions {
	my ($uid, $cnt) = @_;
	my $query = sprintf("SELECT * FROM tracked_routes WHERE user_id = %d ORDER BY logdate DESC limit %d", $uid, $cnt );
	my $sth = $dbh->prepare($query);
	$sth->execute();
	
	return $sth->fetchall_arrayref( {} );
}


sub print_rah {
	my( $rah, $ra_keys ) = @_;
	return if not ($rah || @$rah);
	
	if( $rh_params->{format} eq 'html' ) {
		my $i=0;;
		$_->{'#'} = ++$i for @$rah; 

		my @keys = $ra_keys ? @$ra_keys : keys %{ $rah->[0] };
		unshift @keys, '#';
		print '<div class="rah">';
		print '<table border="1"><tr>';
		print "<th>$_</th>" for @keys;
		print '</tr>';

		for my $rh ( @$rah ) {
			print '<tr>';
			print "<td>$_</td>" for map { $rh->{$_} } @keys;
			print '</tr>';
		}
		print '</table></div>';
	} elsif ( $rh_params->{format} eq 'json' ) {
		print JSON::XS::encode_json( $rah );
	}
}
