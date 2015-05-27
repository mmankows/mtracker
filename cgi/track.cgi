#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5 
use strict;
use warnings;

use lib '/home/eaiibgrp/mmankows/mtracker/lib';
use Data::Dumper;
use CGI;
use CGI::Pretty qw/:standard/;
use DBI;
use URI::Escape;
use MIME::Base64 ();
use JSON::XS;

use DBTools;
use User;
# -d_id(string)    : device id
# -cs (string md5) : control sum
# -lat (base 65 float)
# -lon (base64 float)

my $json_req;	
my $json_resp = { status => 'ERR' };
my $query = CGI->new;

if( $query->request_method eq 'POST') {
    
    # Process registration request
    eval { 
        
	$json_req = $query->param('POSTDATA');
	$json_req = decode_json( $json_req );
	
	# wrong json format
	die "ERR: INVALID JSON\n" if 0
       				     || (not $json_req)    		      
				     || (grep { not $json_req->{ $_ } } qw/token device_id coords/) 		     
				     || (ref $json_req->{coords} ne 'ARRAY') 		    		     
				     || (grep { !$_->{lat} || !$_->{lon} || !$_->{ld} } @{ $json_req->{coords} } );
	# Invalid token
	die "ERR: BAD TOKEN"      if not User::is_valid_token( $json_req );
    };

    # Validation is fine
    if ( not $@ ) {

	# sort to insert starting from oldest logged points
	my $rah_positions = [ sort { $a->{ld} cmp $b->{ld} } @{ $json_req->{coords} } ];
	my $user_id = User::did2uid( $json_req->{device_id} );

	foreach my $pos ( @$rah_positions ) {
		DBTools::save_params( { user_id => $user_id, latitude => $pos->{lat}, longitude => $pos->{lon}, logdate => $pos->{ld} }, 'tracked_routes' );
	}

	$json_resp->{status} = "OK";
    	print header(-type => "application/json", -status => "200 OK" );
    	print Dumper $json_req;
	print Dumper $json_resp;
    } 
    # Some problems encountered
    else {
    	print header(-type => "application/json", -status => "500 ERROR" );
	$json_resp->{status} = $@;
	print Dumper $json_req;
	print Dumper $json_resp;
    }
    
    print encode_json( $json_resp );

} else {
        print header(-type => "text/html", -status => "404 NOT FOUND");
        print "Unsupported request type";
}

