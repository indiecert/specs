<?php

/**
 * Autoloader for indiecert/enroll.
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
    'fkooman\\IndieCert\\Enroll' => dirname(dirname(dirname(__DIR__))),
));

require_once $vendorDir.'/fkooman/Ini/autoload.php';
require_once $vendorDir.'/fkooman/IO/autoload.php';
require_once $vendorDir.'/fkooman/Rest/autoload.php';
require_once $vendorDir.'/fkooman/Tpl/Twig/autoload.php';
require_once $vendorDir.'/phpseclib/autoload.php';
