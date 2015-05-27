package User;
use strict;
use warnings;

use DBTools;

#Check if proper token was sent
sub is_valid_token {
        my %P = @_;

	my $token     = $P{token} || '';
	my $device_id = $P{device_id};
	
	my $user = get_user( device_id => $device_id );
	
	return $token eq $user->{token};
}

#Fetch all information related to user
sub get_user {
	my %P = @_;

	my $dbh = DBTools::db_connect();
	my $sql = 'SELECT * FROM users WHERE device_id = ?';

	return $dbh->selectrow_hashref($sql, {}, $P{ device_id } );
}

#Save user to database
sub save_user {
	my %P = @_;
	
	my $dbh = DBTools::db_connect();
	my $sql = 'INSERT INTO users (login, pass, token, device_id) VALUES (?,?,?,?)';
	
	return $dbh->do($sql, undef, $P{login}, Digest::MD5::md5_hex( $P{pass} ), $P{token}, $P{device_id} );
}

sub did2uid {
	my( $device_id ) = shift;

	my $dbh = DBTools::db_connect();
	my ($user_id) = $dbh->selectrow_array("SELECT user_id FROM users WHERE device_id = '$device_id'");
	return $user_id;
}


1;
