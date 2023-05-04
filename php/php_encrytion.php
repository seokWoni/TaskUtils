<?

    // AES-256-CBC 암호화/복호화
    function hex2bin($hexdata)
    {
        $bindata="";
        for ($i=0;$i<strlen($hexdata);$i+=2)
        {
            $bindata.=chr(hexdec(substr($hexdata,$i,2)));
        }
        return $bindata;
    }

    function iv_encrypt()
    {
        $str = md5(md5(hex2bin("init_vector")));
        $iv_str = md5(md5(hex2bin($str)));
        return $iv_str;
    }

    function encrypt($str, $secret_key, $secret_iv='init_vector')
    {
        $key = substr(md5(md5($secret_key)), 0, 256 / 8);
        $iv  = substr(iv_encrypt(), 0, 16);
        $encrypted = openssl_encrypt($str, "aes-256-cbc", $key, 0, $iv);
        $encrypted = base64_encode(urlencode($encrypted));

        return $iv.'.'.$encrypted;
    }

    function decrypt($str, $secret_key)
    {
        list($iv, $encryptedData) = explode('.' , $str);
        $key = substr(md5(md5($secret_key)), 0, 256 / 8);
        try{
            $decrypted = openssl_decrypt(
                urldecode(base64_decode($encryptedData)), "AES-256-CBC", $key, 0, $iv
            );
        }catch(\Exception $e){
            $decrypted = $str;
        }

        return $decrypted;
    }

>
