package DBTools;






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


1;
