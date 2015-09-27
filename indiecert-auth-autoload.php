<?php

/**
 * Autoloader for indiecert/auth.
 */
$vendorDir = '/usr/share/php';

// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir.'/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}
$fedoraClassLoader->addPrefixes(array(
    'fkooman\\IndieCert\\Auth' => dirname(dirname(dirname(__DIR__))),
));

require_once $vendorDir.'/fkooman/Ini/autoload.php';
require_once $vendorDir.'/fkooman/IO/autoload.php';
require_once $vendorDir.'/fkooman/Rest/autoload.php';
require_once $vendorDir.'/fkooman/Rest/Plugin/Authentication/IndieAuth/autoload.php';
require_once $vendorDir.'/fkooman/Rest/Plugin/Authentication/Tls/autoload.php';
require_once $vendorDir.'/fkooman/Tpl/Twig/autoload.php';
require_once $vendorDir.'/GuzzleHttp/autoload.php';

// https://bugzilla.redhat.com/show_bug.cgi?id=1264987
require_once $vendorDir.'/React/Promise/autoload.php';
