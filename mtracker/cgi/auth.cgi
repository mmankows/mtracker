#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5 

use strict;
use warnings;

use lib '../lib';
use JSON::XS;
use CGI;
use CGI::Pretty qw/:standard/;
use CGI::Cookie;

use Encoding;
use DBTools;
use User;


my $query = CGI->new;

# Submited form, login request sent
if( $query->request_method() eq 'POST' ) {
    
    my $cookie = [];
    # Process login-in request
    eval { 
        
        my $login = $query->param('login');
	my $pass  = $query->param('pass');
	die "Bad parameters!" if not $login and $pass;


	# authentication
	my $user = User::get_user( login => $login )  || die "There's not such user\n";
	$user->{ pass } eq Encoding::hash_pw( $pass ) || die "Wrong password\n";

	# set proper cookies
	push @$cookie, CGI::Cookie->new(-name => 'token', -value => $user->{ token } );
	push @$cookie, CGI::Cookie->new(-name => 'uid',   -value => $user->{ user_id } );
	

    };

    # Validation is fine
    if ( not $@ ) {
	print $query->redirect( -url => '../html/map.html', -cookie => $cookie );
    } 
    # Some problems encountered
    else {
    	print header(-type => "text/html", -status => "500 ERROR" );
	print $@;
    }
    

# standard view
} else {
	# log out - make cookie outdated
	my $new_cookie = [];
	if( $query->param('logout') == 1 ) {
	    	my %cookie = CGI::Cookie->fetch;
		push @$new_cookie, CGI::Cookie->new(-name => 'token', -value => $cookie{ token }{value}, -expires=>'0');
		push @$new_cookie, CGI::Cookie->new(-name => 'uid',   -value => $cookie{ uid }{value},   -expires=>'0' );
	}

        print header(-type => "text/html", -status => "200 OK", -cookie => $new_cookie);
        print q{
	<html>
	<body>
		<form action="auth.cgi" method="POST">
			Podaj login: 
			<br><input type="text"   name="login"><br>
			Podaj haslo: 
			<br><input type="password" name="pass"><br>
			<br><input type="submit" value="Zaloguj">
		</form>
	</body>
	<html>

	};
}
