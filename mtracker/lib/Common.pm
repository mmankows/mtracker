package Common;
use strict;
use warnings;

use JSON::XS;
use DBTools;

sub print_rah {
	my( $rah, $ra_keys, $rh_params ) = @_;
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

# save haash to the table. Hash keys names must be exactly like columns' names
sub get_positions {
	my %P = @_;
	return {} if not %P;

	my $time = '';
	$time .= " AND logdate >= '$P{begin}' " if $P{begin};
	$time .= " AND logdate <= '$P{end}'   " if $P{end};

	my $query = sprintf("SELECT * FROM tracked_routes WHERE user_id = %d $time ORDER BY logdate DESC limit %d", $P{uid}, $P{cnt} );
	
	my $dbh = DBTools::db_connect();
	my $sth = $dbh->prepare($query);
	$sth->execute();
	
	return $sth->fetchall_arrayref( {} );
}

1;
