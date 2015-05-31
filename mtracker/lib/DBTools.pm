package DBTools;
use strict;
use warnings;

use DBI;
use Digest::MD5;
use Data::Dumper;

# Connect to database 
sub db_connect {
	my %params = @_ ||  (
		host => 'data.uci.agh.edu.pl',
		user => 'mmankow1',
		pass => 'xn4HsR7f',
		db   => 'mmankow1',
	);

	my $conn_str = sprintf("DBI:mysql:database=%s;host=%s", $params{db}, $params{host} );
	my $dbh      = DBI->connect($conn_str,$params{user}, $params{pass}, { RaiseError => 1 } ) or die(DBI->errstr);

	return $dbh;
}

sub save_params {
	my ($rh_params, $table_name) = @_;
	return {} if not keys %$rh_params;
	my $query = sprintf("INSERT INTO %s (%s) VALUES (%s)",$table_name, join(',',keys %$rh_params), join(',',map { '?' } values %$rh_params));
	my $dbh = db_connect();
	my $sth = $dbh->prepare($query);
	$sth->execute(values %$rh_params);
	
}
	

1;
