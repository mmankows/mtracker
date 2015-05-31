package Encoding;
use strict;
use warnings;
use Digest::MD5;


sub calc_cs {
	my %P = @_;
	my $cs = '';
	$cs = ( $P{login} | $P{pass} ) ^ $P{did};

	return Digest::MD5::md5_base64( $cs );
}

sub validate_cs {
	my %P = @_;
	
	my $imho_sum = calc_cs( %P );
	return $imho_sum eq $P{ cs };
}

sub gen_token {
	my %P = @_;
	my $token = $P{ cs };
	$token = Digest::MD5::md5_hex( $token ) for 1..3;
	return $token;
}



1;
