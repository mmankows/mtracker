#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5 
use strict;
use warnings;

use lib '/home/eaiibgrp/mmankows/mtracker/lib';
use JSON::XS;
use CGI;
use CGI::Pretty qw/:standard/;

use Encoding;
use DBTools;


my $json_req;	
my $json_resp = { status => 'ERR' };
my $query = CGI->new;

if( $query->request_method eq 'POST') {
    
    # Process registration request
    eval { 
        
	$json_req = $query->param('POSTDATA');
        
	$json_req = decode_json( $json_req );
	
	# wrong json format
	$json_resp->{ status } = "ERR: INVALID JSON",  die "\n" if not $json_req || grep { not $json_req->{ $_ } } qw/login pass did cs/;
	# already has such device id
	$json_resp->{ status } = "ERR: ALREADY EXISTS",die "\n" if DBTools::get_user( device_id => $json_req->{did} );
	# wrong control sum (mallicious user?)
	$json_resp->{ status } = "ERR: WRONG PARAMS",  die "\n" if not Encoding::validate_cs( %$json_req );

	$json_resp->{ token }  = Encoding::gen_token( %$json_req ); 

    };

    # Validation is fine
    if ( not $@ ) {
	DBTools::save_user( device_id => $json_req->{did}, login => $json_req->{login}, pass => $json_req->{pass}, token => $json_resp->{token} );
	$json_resp->{status} = "OK";
    	print header(-type => "application/json", -status => "200 OK" );
    } 
    # Some problems encountered
    else {
    	print header(-type => "application/json", -status => "500 ERROR" );
    }
    
    print encode_json( $json_resp );

} else {
        print header(-type => "text/html", -status => "404 NOT FOUND");
        print "Unsupported request type";
}
