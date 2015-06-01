package User;
use strict;
use warnings;

use DBTools;
use Encoding;

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
	
        my $sel   = $P{ user_id }   ? 'user_id' : '';
	   $sel ||= $P{ device_id } ? 'device_id' : '';
	   $sel ||= $P{ login     } ? 'login' : '';

	my $val = $P{ user_id } || $P{ device_id } ||  $P{ login } || '';

	return {} if not $val && $sel;

	my $dbh = DBTools::db_connect();
	my $sql = "SELECT * FROM users WHERE $sel = ?";

	return $dbh->selectrow_hashref($sql, {}, $val );
}

#Save user to database
sub save_user {
	my %P = @_;
	
	my $dbh = DBTools::db_connect();
	my $sql = 'INSERT INTO users (login, pass, token, device_id) VALUES (?,?,?,?)';
	
	#return $dbh->do($sql, undef, $P{login}, Digest::MD5::md5_hex( $P{pass} ), $P{token}, $P{device_id} );
	return $dbh->do($sql, undef, $P{login}, Encoding::hash_pw( $P{pass} ), $P{token}, $P{device_id} );
}

sub did2uid {
	my( $device_id ) = shift;

	my $dbh = DBTools::db_connect();
	my ($user_id) = $dbh->selectrow_array("SELECT user_id FROM users WHERE device_id = '$device_id'");
	return $user_id;
}

sub uid2did {
	my( $user_id ) = shift;

	my $dbh = DBTools::db_connect();
	my ($device_id) = $dbh->selectrow_array("SELECT device_id FROM users WHERE user_id = '$user_id'");
	return $device_id;
}


1;